from allpairspy import AllPairs

parameters = [
    ["Windows", "Linux", "macOS"],
    ["Intel", "AMD"],
    [8, 16]
]

# Генерация тестовых комбинаций
for pair in AllPairs(parameters):
    print(pair)  # Например: ('Windows', 'Intel', 8)
