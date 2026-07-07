import sys
from PIL import Image, ImageDraw

CELL_SIZE = 20
PADDING = 2
MAX_AGE = 10


def read_init(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines2 = [line.strip() for line in lines if line.strip()]
    first = lines2[0].split()
    rows = int(first[0])
    cols = int(first[1])
    grid = []
    for i in range(1, rows + 1):
        row = [int(val) for val in lines2[i].split()]
        grid.append(row)
    
    return grid


def count_live_neighbors(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    if row - 1 >= 0 and col - 1 >= 0:
        if grid[row - 1][col - 1] == 1:
            count += 1
    
    if row - 1 >= 0:
        if grid[row - 1][col] == 1:
            count += 1
    
    if row - 1 >= 0 and col + 1 < cols:
        if grid[row - 1][col + 1] == 1:
            count += 1
    
    if col - 1 >= 0:
        if grid[row][col - 1] == 1:
            count += 1
    
    if col + 1 < cols:
        if grid[row][col + 1] == 1:
            count += 1
    
    if row + 1 < rows and col - 1 >= 0:
        if grid[row + 1][col - 1] == 1:
            count += 1
    
    if row + 1 < rows:
        if grid[row + 1][col] == 1:
            count += 1
    
    if row + 1 < rows and col + 1 < cols:
        if grid[row + 1][col + 1] == 1:
            count += 1
    
    return count


def life_step_with_age(grid, age_grid):
    rows = len(grid)
    cols = len(grid[0])
    
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    new_age_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for row in range(rows):
        for col in range(cols):
            neighbors = count_live_neighbors(grid, row, col)
            
            if grid[row][col] == 1: 
                if neighbors == 2 or neighbors == 3:
                    new_grid[row][col] = 1
                    new_age_grid[row][col] = age_grid[row][col] + 1  
                else:
                    new_grid[row][col] = 0
                    new_age_grid[row][col] = 0
            else:  
                if neighbors == 3:
                    new_grid[row][col] = 1
                    new_age_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
                    new_age_grid[row][col] = 0
    
    return new_grid, new_age_grid


def get_cell_color(base_color, age, max_age=MAX_AGE):
    r, g, b = base_color
    factor = max(0.2, 1.0 - (age / max_age))
    return (int(r * factor), int(g * factor), int(b * factor))


def simulation(grid, num_generations):
    rows = len(grid)
    cols = len(grid[0])
    
    all_history = [grid]
    age_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    all_ages = [age_grid]
    
    for _ in range(num_generations):
        grid, age_grid = life_step_with_age(grid, age_grid)
        all_history.append(grid)
        all_ages.append(age_grid)
    
    return all_history, all_ages


def save_output_csv(full_grid):
    for step in range(len(full_grid)):
        grid = full_grid[step]
        filename = f"output_{step:03d}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Generation {step}\n")
            for row in grid:
                f.write(' '.join(map(str, row)) + '\n')


def save_output_png(full_grid, full_ages, base_color=(0, 255, 0)):
    for step in range(len(full_grid)):
        grid = full_grid[step]
        ages = full_ages[step]
        rows = len(grid)
        cols = len(grid[0])
        
        img_width = cols * (CELL_SIZE + PADDING) + PADDING
        img_height = rows * (CELL_SIZE + PADDING) + PADDING
        
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for row in range(rows):
            for col in range(cols):
                x = col * (CELL_SIZE + PADDING) + PADDING
                y = row * (CELL_SIZE + PADDING) + PADDING
                
                if grid[row][col] == 1:
                    age = ages[row][col]
                    color = get_cell_color(base_color, age)
                    draw.rectangle([x, y, x + CELL_SIZE, y + CELL_SIZE], fill=color)
        
        for col in range(cols + 1):
            x = col * (CELL_SIZE + PADDING) + PADDING
            draw.line([(x, PADDING), (x, img_height - PADDING)], fill=(200, 200, 200), width=1)
        
        for row in range(rows + 1):
            y = row * (CELL_SIZE + PADDING) + PADDING
            draw.line([(PADDING, y), (img_width - PADDING, y)], fill=(200, 200, 200), width=1)
        
        filename = f"output_{step:03d}.png"
        img.save(filename)


def main():
    input_file = "input_life.csv"
    base_color = (0, 255, 0)
    
    while True:
        try:
            user_input = input("Введите количество поколений (Enter = 10): ")
            if user_input == "":
                num_generations = 10
                print(f"Используем {num_generations} поколений (по умолчанию)")
                break
            num_generations = int(user_input)
            if num_generations <= 0:
                print("ОШИБКА: Число должно быть положительным!")
                continue
            break
        except ValueError:
            print("ОШИБКА: Введите целое число!")
    
    try:
        grid = read_init(input_file)
    except FileNotFoundError:
        print(f"ОШИБКА: Файл '{input_file}' не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"ОШИБКА при чтении файла: {e}")
        sys.exit(1)
    
    full_history, full_ages = simulation(grid, num_generations)
    save_output_csv(full_history)
    save_output_png(full_history, full_ages, base_color)
    
    print("Files created!")


if __name__ == '__main__':
    main()