import numpy as np
from collections import Counter, defaultdict

def entropy(y):
    m = len(y)
    if m == 0:
        return 0.0
    counts = np.array(list(Counter(y).values()), dtype=float)
    p = counts / m

    return -np.sum(np.where(p > 0, p * np.log2(p), 0.0))

def info_gain(parent_y, left_y, right_y):
    n = len(parent_y)
    nL, nR = len(left_y), len(right_y)
    if nL == 0 or nR == 0:
        return 0.0
    return entropy(parent_y) - (nL/n)*entropy(left_y) - (nR/n)*entropy(right_y)

class _TreeNode:
    __slots__ = ("feature", "threshold", "left", "right", "value")
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature   = feature
        self.threshold = threshold
        self.left      = left
        self.right     = right
        self.value     = value

class DecisionTreeClassifierScratch:
    def __init__(self, max_depth=None, min_samples_split=2, max_features=None, random_state=None):

        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.root = None
        self.rng = np.random.default_rng(random_state)

    def _majority_class(self, y):
        return Counter(y).most_common(1)[0][0]

    def _feature_subset(self, n_features):
        if self.max_features is None:
            k = n_features
        elif self.max_features == 'sqrt':
            k = max(1, int(np.sqrt(n_features)))
        elif isinstance(self.max_features, int):
            k = max(1, min(self.max_features, n_features))
        else:
            raise ValueError("max_features must be None, 'sqrt', or int")
        return self.rng.choice(n_features, size=k, replace=False)

    def _best_split(self, X, y, features_idx):
        m, n = X.shape
        if m < self.min_samples_split:
            return None, None, 0.0

        best_feat, best_thr, best_gain = None, None, 0.0
        parent_y = y

        for f in features_idx:
            x_f = X[:, f]
            order = np.argsort(x_f, kind="mergesort")
            x_sorted = x_f[order]
            y_sorted = parent_y[order]

            unique_mask = np.diff(x_sorted) > 0
            if not np.any(unique_mask):
                continue

            # running counts for left split
            left_counts = defaultdict(int)
            right_counts = Counter(y_sorted)
            left_size = 0
            right_size = len(y_sorted)

            for i in range(len(x_sorted) - 1):
                cls = y_sorted[i]
                left_counts[cls] += 1
                right_counts[cls] -= 1
                left_size += 1
                right_size -= 1

                if not unique_mask[i]:
                    continue

                thr = (x_sorted[i] + x_sorted[i+1]) / 2.0

                y_left = y_sorted[:left_size]
                y_right = y_sorted[left_size:]

                gain = info_gain(parent_y, y_left, y_right)
                if gain > best_gain:
                    best_gain, best_feat, best_thr = gain, f, thr

        return best_feat, best_thr, best_gain

    def _build(self, X, y, depth):
        if (self.max_depth is not None and depth >= self.max_depth) or len(set(y)) == 1 or len(y) < self.min_samples_split:
            return _TreeNode(value=self._majority_class(y))

        features_idx = self._feature_subset(X.shape[1])
        feat, thr, gain = self._best_split(X, y, features_idx)

        if feat is None or gain <= 0.0:
            return _TreeNode(value=self._majority_class(y))


        left_mask = X[:, feat] <= thr
        right_mask = ~left_mask
        left_child = self._build(X[left_mask], y[left_mask], depth+1)
        right_child = self._build(X[right_mask], y[right_mask], depth+1)
        return _TreeNode(feature=feat, threshold=thr, left=left_child, right=right_child)

    def fit(self, X, y):
        X = np.asarray(X)
        y = np.asarray(y)
        self.root = self._build(X, y, depth=0)
        return self

    def _predict_one(self, x, node):
        while node.value is None:
            node = node.left if x[node.feature] <= node.threshold else node.right
        return node.value

    def predict(self, X):
        X = np.asarray(X)
        return np.array([self._predict_one(row, self.root) for row in X])



class RandomForestScratch:
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2,
                 max_features='sqrt', bootstrap=True, random_state=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.trees = []
        self.rng = np.random.default_rng(random_state)

    def _bootstrap_sample(self, X, y):
        m = X.shape[0]
        idx = self.rng.integers(0, m, size=m) if self.bootstrap else np.arange(m)
        return X[idx], y[idx]

    def fit(self, X, y):
        X = np.asarray(X)
        y = np.asarray(y)
        self.trees = []
        for i in range(self.n_estimators):
            Xi, yi = self._bootstrap_sample(X, y)
            tree = DecisionTreeClassifierScratch(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features,
                random_state=self.rng.integers(0, 1_000_000)
            )
            tree.fit(Xi, yi)
            self.trees.append(tree)
        return self

    def predict(self, X):
        X = np.asarray(X)
        preds = np.stack([t.predict(X) for t in self.trees], axis=1)
        out = []
        for row in preds:
            out.append(Counter(row).most_common(1)[0][0])
        return np.array(out)
