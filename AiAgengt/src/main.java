public class main {

    public static void main(String[] args) {

        Grid grid = new Grid(5, 4);
        UtilityAgent agent = new UtilityAgent(0, 0);

        int steps = 0;

        while (grid.anyDirtLeft() && steps < 100) {

            System.out.println("Step: " + steps);
            grid.display(agent.x, agent.y);

            agent.act(grid);

            steps++;
        }

        System.out.println("All clean or max steps reached!");
    }
}