public class UtilityAgent {

    int x, y;
    double rewardClean = 10.0;
    double moveCost = 1.0;
    double timePenalty = 0.1;

    public UtilityAgent(int startX, int startY) {
        this.x = startX;
        this.y = startY;
    }

    public void act(Grid grid) {

        // If current tile is dirty then clean it
        if (grid.isDirty(x, y)) {
            grid.clean(x, y);
            System.out.println("Cleaning at (" + x + "," + y + ")");
            return;
        }

        // Otherwise choose best move using utility
        int[][] moves = {
                {x + 1, y},
                {x - 1, y},
                {x, y + 1},
                {x, y - 1}
        };

        double bestUtility = -Double.MAX_VALUE;
        int bestX = x;
        int bestY = y;

        for (int[] move : moves) {
            int newX = move[0];
            int newY = move[1];

            if (newX >= 0 && newX < grid.width &&
                    newY >= 0 && newY < grid.height) {

                double utility = calculateUtility(grid, newX, newY);

                if (utility > bestUtility) {
                    bestUtility = utility;
                    bestX = newX;
                    bestY = newY;
                }
            }
        }

        x = bestX;
        y = bestY;

        System.out.println("Moving to (" + x + "," + y + ")");
    }

    private double calculateUtility(Grid grid, int newX, int newY) {

        double immediateCost = moveCost + timePenalty;

        int nearestDistance = findNearestDirt(grid, newX, newY);

        if (nearestDistance == -1) {
            return -1000;
        }

        double futureReward = rewardClean - (nearestDistance * moveCost);

        return futureReward - immediateCost;
    }

    private int findNearestDirt(Grid grid, int x, int y) {

        int minDistance = Integer.MAX_VALUE;

        for (int i = 0; i < grid.width; i++) {
            for (int j = 0; j < grid.height; j++) {

                if (grid.isDirty(i, j)) {
                    int distance = Math.abs(i - x) + Math.abs(j - y);
                    if (distance < minDistance) {
                        minDistance = distance;
                    }
                }
            }
        }

        if (minDistance == Integer.MAX_VALUE)
            return -1;

        return minDistance;
    }
}
