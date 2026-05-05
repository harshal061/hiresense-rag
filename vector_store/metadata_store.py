class MetadataStore:
    def __init__(self):
        self.data = []

    def add(self, item):
        self.data.append(item)

    def get(self, idx):
        return self.data[idx]

    def get_multiple(self, indices):
        return [self.data[i] for i in indices if i < len(self.data)]