import java.util.*;

public class CScanDiskScheduling {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input disk requests and parameters
        System.out.print("Enter number of requests: ");
        int n = sc.nextInt();
        int[] requests = new int[n];
        System.out.println("Enter requests: ");
        for (int i = 0; i < n; i++) {
            requests[i] = sc.nextInt();
        }

        System.out.print("Enter initial head position: ");
        int head = sc.nextInt();
        System.out.print("Enter disk size: ");
        int diskSize = sc.nextInt();

        // Sort requests
        Arrays.sort(requests);
        List<Integer> left = new ArrayList<>();
        List<Integer> right = new ArrayList<>();
        for (int request : requests) {
            if (request < head) left.add(request);
            else right.add(request);
        }

        // Process requests
        int totalSeekTime = 0;
        List<Integer> seekOrder = new ArrayList<>();

        // Process right side
        for (int request : right) {
            seekOrder.add(request);
            totalSeekTime += Math.abs(head - request);
            head = request;
        }

        // Reset head to start
        totalSeekTime += Math.abs(diskSize - 1 - head) + (diskSize - 1);
        head = 0;

        // Process left side
        for (int request : left) {
            seekOrder.add(request);
            totalSeekTime += Math.abs(head - request);
            head = request;
        }

        // Output results
        System.out.println("Seek Order: " + seekOrder);
        System.out.println("Total Seek Time: " + totalSeekTime);

        sc.close();
    }
}