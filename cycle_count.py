import torch

def find_cycles(edge_index, edge_type):
    num_nodes = edge_index.max().item() + 1  # 최대 노드 번호 + 1

    adj_list = {i: [] for i in range(num_nodes)}
    edge_type_dict = {}

    # 인접 리스트 및 엣지 타입 저장
    for i, (source, target) in enumerate(edge_index.T.tolist()):
        adj_list[source].append(target)
        edge_type_dict[(source, target)] = edge_type[i]

    def find_cycles_dfs(node, start_node, depth, visited, path, cycles):
        visited.add(node)
        path.append(node)

        if depth >= 2:
            for neighbor in adj_list[node]:
                if neighbor == start_node and ((start_node, node) in edge_type_dict or (node, start_node) in edge_type_dict):
                    cycle = list(path)
                    min_idx = cycle.index(min(cycle))
                    cycle = cycle[min_idx:] + cycle[:min_idx]
                    cycles.add(tuple(cycle))

        if depth < 3:  # 깊이 3까지 탐색
            for neighbor in adj_list[node]:
                if neighbor not in visited:
                    find_cycles_dfs(neighbor, start_node, depth + 1, visited, path, cycles)

        path.pop()
        visited.remove(node)

    cycles = set()
    for start_node in range(num_nodes):
        find_cycles_dfs(start_node, start_node, 0, set(), [], cycles)

    return [list(cycle) for cycle in cycles]

if __name__ == '__main__':
    
    # 🚀 간단한 양방향 그래프 예제
    edge_index = torch.tensor([
        [0, 1, 1, 3, 3, 2, 2, 0],  # 출발 노드
        [1, 0, 3, 1, 2, 3, 0, 2]   # 도착 노드 (양방향 포함)
    ])  # bidirectional

    edge_type = torch.tensor([1, 1, 2, 2, 3, 3, 4, 4])

    cycles = find_cycles(edge_index, edge_type)
    print("Detected Cycles:", cycles)
