import sys
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("ОШИБКА: Библиотека Pillow не установлена!")

NUM_OF_GENERATIONS = 10

def read_init(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    lines2 = []
    for line in lines:
        if line.strip():
            lines2.append(line.strip())
    
    first = lines2[0].split()
    rows = int(first[0])
    cols = int(first[1])

    grid = []
    for i in range(1, rows + 1):
        row = lines2[i].split()
        row_int = []
        for val in row:
            row_int.append(int(val))
        grid.append(row_int)
    
    return grid

def count_live_neighbors(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    if row - 1 >= 0 and col - 1 >= 0:
        if grid[row - 1][col - 1] == 1:
            count = count + 1
    if row - 1 >= 0:
        if grid[row - 1][col] == 1:
            count = count + 1
    if row - 1 >= 0 and col + 1 < cols:
        if grid[row - 1][col + 1] == 1:
            count = count + 1
    if col - 1 >= 0:
        if grid[row][col - 1] == 1:
            count = count + 1
    if col + 1 < cols:
        if grid[row][col + 1] == 1:
            count = count + 1
    if row + 1 < rows and col - 1 >= 0:
        if grid[row + 1][col - 1] == 1:
            count = count + 1
    if row + 1 < rows:
        if grid[row + 1][col] == 1:
            count = count + 1
    if row + 1 < rows and col + 1 < cols:
        if grid[row + 1][col + 1] == 1:
            count = count + 1
    
    return count

def life_step(grid):
    rows = len(grid)
    cols = len(grid[0])

    new_grid = []
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(0)
        new_grid.append(new_row)

    for row in range(rows):
        for col in range(cols):
            neighbors = count_live_neighbors(grid, row, col)
            
            if grid[row][col] == 1:
                if neighbors == 2 or neighbors == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
            else:
                if neighbors == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
    
    return new_grid

def simulation(grid):
    all_history = []
    all_history.append(grid)
    
    for step in range(NUM_OF_GENERATIONS):
        grid = life_step(grid)
        all_history.append(grid)
    
    return all_history

def save_output_csv(full_grid):
    for step in range(len(full_grid)):
        grid = full_grid[step]
        filename = "output_" + str(step).zfill(3) + ".txt"
        
        f = open(filename, 'w')
        f.write("Generation " + str(step) + "\n")
        
        for row in range(len(grid)):
            row_str = ""
            for col in range(len(grid[row])):
                row_str = row_str + str(grid[row][col]) + " "
            row_str = row_str.strip()
            f.write(row_str + "\n")
        
        f.close()

def save_output_png(full_grid, base_color=(0, 255, 0)):
    cell_size = 20
    padding = 2
    grid_color = (200, 200, 200)
    
    for step in range(len(full_grid)):
        grid = full_grid[step]
        rows = len(grid)
        cols = len(grid[0])
        
        img_width = cols * (cell_size + padding) + padding
        img_height = rows * (cell_size + padding) + padding
        
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)

        for row in range(rows):
            for col in range(cols):
                x = col * (cell_size + padding) + padding
                y = row * (cell_size + padding) + padding
                
                if grid[row][col] == 1:
                    draw.rectangle([x, y, x + cell_size, y + cell_size], fill=base_color)
        
        for col in range(cols + 1):
            x = col * (cell_size + padding) + padding
            draw.line([(x, padding), (x, img_height - padding)], fill=grid_color, width=1)
        
        for row in range(rows + 1):
            y = row * (cell_size + padding) + padding
            draw.line([(padding, y), (img_width - padding, y)], fill=grid_color, width=1)
        
        filename = "output_" + str(step).zfill(3) + ".png"
        img.save(filename)

def main():
    input_file = "input_life.csv"
    base_color = (0, 255, 0)
    
    grid = read_init(input_file)
    full_history = simulation(grid)
    save_output_csv(full_history)
    save_output_png(full_history, base_color)
    
    print("Files created!")

if __name__ == '__main__':
    main()