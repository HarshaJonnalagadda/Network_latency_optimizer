from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AnalysisResult
from projects.models import Project
from pcap_upload.models import PcapFile
import scapy.all as scapy
import networkx as nx
import numpy as np
from sklearn.svm import OneClassSVM
from django.core.serializers.json import DjangoJSONEncoder
import json

@api_view(['POST'])
def analyze_project(request, project_id):
    """
    Analyze the PCAP files of a project using One-Class SVM for anomaly detection
    and Dijkstra's Algorithm for path optimization.
    """
    # Fetch the project by ID
    project = get_object_or_404(Project, pk=project_id)
    pcap_files = project.pcap_files.all()

    if not pcap_files:
        return Response({"error": "No PCAP files available for analysis."}, status=status.HTTP_400_BAD_REQUEST)

    # List to store latencies and edges for the network graph
    latencies = []
    edges = []
    network_graph = nx.Graph()

    # Step 1: Analyze PCAP files and gather latencies and network connections
    for pcap_file in pcap_files:
        file_path = pcap_file.file.path

        try:
            packets = scapy.rdpcap(file_path)
            for i in range(len(packets) - 1):
                packet1 = packets[i]
                packet2 = packets[i + 1]

                # Calculate latency if both packets have timestamps
                if hasattr(packet1, 'time') and hasattr(packet2, 'time'):
                    latency = float(packet2.time - packet1.time)
                    src_ip = packet1[scapy.IP].src if packet1.haslayer(scapy.IP) else None
                    dst_ip = packet2[scapy.IP].dst if packet2.haslayer(scapy.IP) else None

                    if src_ip and dst_ip:
                        latencies.append((src_ip, dst_ip, latency))
                        edges.append((src_ip, dst_ip, latency))
        except Exception as e:
            return Response({"error": f"Error reading PCAP file {pcap_file.file.name}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Check if we have enough latency data for analysis
    if len(latencies) < 2:
        return Response({"error": "Not enough latency data for analysis."}, status=status.HTTP_400_BAD_REQUEST)

    # Step 2: Convert latencies to a NumPy array and reshape for One-Class SVM
    latency_values = np.array([latency for _, _, latency in latencies]).reshape(-1, 1)

    # Train One-Class SVM for anomaly detection
    try:
        model = OneClassSVM(kernel="rbf", gamma='auto', nu=0.05)  # nu: proportion of anomalies expected
        model.fit(latency_values)

        # Predict anomalies (-1 indicates anomalies, 1 indicates normal data)
        predictions = model.predict(latency_values)

        # Identify anomalous paths
        anomalous_paths = [
            (src, dst, latency) for (src, dst, latency), pred in zip(latencies, predictions) if pred == -1
        ]
    except Exception as e:
        return Response({"error": f"Error during anomaly detection: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Step 3: Build network graph excluding anomalous paths
    for src, dst, latency in edges:
        if (src, dst, latency) not in anomalous_paths:
            network_graph.add_edge(src, dst, weight=latency)

    # Step 4: Optimize paths using Dijkstra's Algorithm
    optimization_results = []
    for src in network_graph.nodes:
        for dst in network_graph.nodes:
            if src != dst and nx.has_path(network_graph, src, dst):
                # Current latency
                current_latency = sum(lat for s, d, lat in edges if (s, d) == (src, dst) or (d, s) == (src, dst))
                
                # Optimized path
                shortest_path = nx.shortest_path(network_graph, source=src, target=dst, weight='weight')
                optimized_latency = nx.shortest_path_length(network_graph, source=src, target=dst, weight='weight')
                
                # Record the result
                optimization_results.append({
                    "source": src,
                    "destination": dst,
                    "current_latency": f"{current_latency:.4f} seconds",
                    "optimized_latency": f"{optimized_latency:.4f} seconds",
                    "optimized_path": " -> ".join(shortest_path),
                })

    # Step 5: Store the analysis result in the database
    analysis_result, created = AnalysisResult.objects.update_or_create(
        project=project,
        defaults={
            "anomalies_detected": len(anomalous_paths),
            "average_latency": float(np.mean(latency_values)) * 1000,  # Convert to milliseconds
            "optimizations": json.dumps(optimization_results, cls=DjangoJSONEncoder), 
            #"optimizations": optimization_results,
        },
    )
    print("Optimization Results:", optimization_results)
    # Return the analysis results
    return Response({
        "project_name": project.name,
        "anomalies_detected": analysis_result.anomalies_detected,
        "average_latency": analysis_result.average_latency,
        "optimizations": optimization_results,
        "analyzed_at": analysis_result.analyzed_at,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_analysis_result(request, project_id):
    """
    Get the analysis result of a project.
    """
    # Fetch the project by ID
    project = get_object_or_404(Project, pk=project_id)

    try:
        # Fetch the analysis result for the project
        analysis_result = AnalysisResult.objects.get(project=project)

        optimizations = json.loads(analysis_result.optimizations)
        return Response({
            "project_name": project.name,
            "anomalies_detected": analysis_result.anomalies_detected,
            "average_latency": analysis_result.average_latency,
            "optimizations": optimizations,
            "analyzed_at": analysis_result.analyzed_at,
        }, status=status.HTTP_200_OK)
    except AnalysisResult.DoesNotExist:
        return Response({"error": "No analysis results found for this project."}, status=status.HTTP_404_NOT_FOUND)
