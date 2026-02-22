import java.util.Random;

public class Grid {
    int width;
    int height;
    boolean[][] grid;
    Random rand;

    public Grid(int width, int height) {
        this.width = width;
        this.height = height;
        this.rand = new Random();
        this.grid = new boolean[width][height];
        generateGrid();
    }

    private void generateGrid() {
        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                grid[i][j] = rand.nextBoolean();
            }
        }
    }

    public boolean isDirty(int x, int y) {
        return grid[x][y];
    }

    public void clean(int x, int y) {
        grid[x][y] = false;
    }

    public void display(int agentX, int agentY) {
        for (int j = 0; j < height; j++) {
            for (int i = 0; i < width; i++) {
                if (i == agentX && j == agentY) {
                    System.out.print("A ");
                } else if (grid[i][j]) {
                    System.out.print("* ");
                } else {
                    System.out.print(". ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }

    public boolean anyDirtLeft() {
        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                if (grid[i][j]) return true;
            }
        }
        return false;
    }
}