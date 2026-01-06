import numpy as np
from scipy.spatial import distance_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import networkx as nx
from collections import Counter
def mst_clustering(X, dist_thresh, min_cluster_size=3, purity_thresh=0.6,
                   labeled_idx=None, y_labeled=None, outlier_factor=2.0,
                   reassign_outliers=True):

    n = len(X)
    # Distance matrix
    D = distance_matrix(X, X)
    mst = minimum_spanning_tree(D)  # MST
    edges = [(i, j, D[i, j]) for i, j in zip(*mst.nonzero())]

    # Build graph with edges <= threshold
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i, j, w in edges:
        if w <= dist_thresh:
            G.add_edge(i, j, weight=w)

    # Connected components = clusters
    clusters = list(nx.connected_components(G))

    cluster_assignments = np.full(n, -1, dtype=int)  # -1 = noise
    cluster_labels = {}
    preds = [None] * n

    # Handle labeled points
    labeled_idx = np.array(labeled_idx) if labeled_idx is not None else np.array([])
    y_labeled = np.array(y_labeled) if y_labeled is not None else np.array([])

    centroids = {}

    # Process clusters
    for cid, comp in enumerate(clusters):
        comp = list(comp)
        if len(comp) < min_cluster_size:
            continue  # too small → noise
        cluster_assignments[comp] = cid

        # Label cluster by majority vote
        labels_in_comp = []
        if labeled_idx.size > 0:
            mask = np.isin(labeled_idx, comp)
            labels_in_comp = list(y_labeled[mask])

        if labels_in_comp:
            c = Counter(labels_in_comp)
            maj_label, maj_count = c.most_common(1)[0]
            purity = maj_count / len(labels_in_comp)
            if purity >= purity_thresh:
                cluster_labels[cid] = maj_label
            else:
                cluster_labels[cid] = None
        else:
            cluster_labels[cid] = None

        # Compute centroid and distances
        centroid = np.mean(X[comp], axis=0)
        centroids[cid] = centroid
        dists = np.linalg.norm(X[comp] - centroid, axis=1)
        cutoff = outlier_factor * np.std(dists)

        for idx, point_idx in enumerate(comp):
            if dists[idx] > cutoff:
                cluster_assignments[point_idx] = -1
                preds[point_idx] = None
            else:
                preds[point_idx] = cluster_labels[cid]

    # Reassign outliers/noise
    if reassign_outliers and centroids:
        for i in range(n):
            if cluster_assignments[i] == -1:
                dists_to_clusters = {cid: np.linalg.norm(X[i] - cent)
                                     for cid, cent in centroids.items()}
                best_cid = min(dists_to_clusters, key=dists_to_clusters.get)
                cluster_assignments[i] = best_cid
                preds[i] = cluster_labels[best_cid]

    return cluster_assignments, cluster_labels, preds




