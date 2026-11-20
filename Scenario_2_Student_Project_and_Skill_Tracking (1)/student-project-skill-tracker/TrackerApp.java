import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.*;

public class TrackerApp {
    private final Scanner input = new Scanner(System.in);
    private String ask(String prompt) {
        System.out.println(prompt);
        String value = input.nextLine().strip();
        if (value.isEmpty()) throw new IllegalArgumentException("A value is required.");
        return value;
    }
    private void save(String... args) throws IOException, InterruptedException {
        List<String> command = new ArrayList<>(List.of(System.getenv().getOrDefault("TRACKER_PYTHON","python"), "store.py"));
        command.addAll(List.of(args));
        new ProcessBuilder(command).inheritIO().start().waitFor();
    }
    private void project() throws Exception {
        List<String> args = new ArrayList<>(List.of("project",ask("Student register number"),ask("Project title"),ask("Domain"),ask("Description")));
        Set<String> names = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
        for (String name : ask("Technologies, separated by commas").split(",")) {
            if (!name.isBlank()) names.add(name.strip());
        }
        if (names.isEmpty()) throw new IllegalArgumentException("Enter a technology.");
        args.addAll(names);
        save(args.toArray(String[]::new));
    }
    private void run() throws Exception {
        while (true) {
            System.out.println("1 Save student | 2 Add skill | 3 Register project | 4 Plan milestone | 5 Submit milestone | 6 Save mark | 7 Reports | 0 Exit");
            if (!input.hasNextLine()) return;
            try {
                switch (ask("Choice")) {
                    case "0" -> {return;}
                    case "1" -> save("student",ask("Register number"),ask("Name"),ask("Department"));
                    case "2" -> save("skill",ask("Register number"),ask("Skill or language"));
                    case "3" -> project();
                    case "4" -> save("milestone",ask("Project ID"),ask("Milestone"),LocalDate.parse(ask("Due date YYYY-MM-DD")).toString());
                    case "5" -> {
                        String id=ask("Project ID"), name=ask("Milestone");
                        LocalDate date=LocalDate.parse(ask("Submission date YYYY-MM-DD"));
                        if (date.isAfter(LocalDate.now())) throw new IllegalArgumentException("Submission date is in the future.");
                        save("submit",date.toString(),id,name);
                    }
                    case "6" -> {
                        String id=ask("Project ID"),component=ask("Component: Design, Implementation or Presentation");
                        int mark=Integer.parseInt(ask("Mark (0 to 100)"));
                        if(mark<0 || mark>100) throw new IllegalArgumentException("Mark must be 0 to 100.");
                        save("mark",id,component,Integer.toString(mark));
                    }
                    case "7" -> save("reports");
                    default -> System.out.println("Select 0 to 7.");
                }
            } catch (DateTimeParseException | IllegalArgumentException ex) {
                System.out.println("Rejected: "+ex.getMessage());
            } catch (NoSuchElementException end) {return;}
        }
    }
    public static void main(String[] args) throws Exception {new TrackerApp().run();}
}
