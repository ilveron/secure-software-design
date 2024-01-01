import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Dealer d = new Dealer();

        Scanner in = new Scanner(System.in);
        byte choice = -1;

        while(choice != 0) {
            printMenu();
            System.out.print("Your choice: ");
            choice = in.nextByte();
            switch (choice){
                case 1:
                    d.addVehicle(inputVehicle("car"));
                    break;

                case 2:
                    d.addVehicle(inputVehicle("motorbike"));
                    break;

                case 3:
                    d.printVehicles();
                    if (d.getVehicleCount() > 0) {
                        System.out.print(System.lineSeparator() + "Please select the index of the vehicle you want to remove: "); int i = in.nextInt();
                        Vehicle toRemove = d.getVehicle(i);
                        if (toRemove != null)
                            d.removeVehicle(toRemove);
                    }
                    break;

                case 4:
                    d.printVehicles();
                    break;

                case 5:
                    d.sortVehiclesByAscendingPrice();
                    d.printVehicles();
                    break;

                case 6:
                    d.sortVehiclesByDescendingPrice();
                    d.printVehicles();
                    break;

                case 7:
                    d.saveToFile("vehicles.txt");
                    break;

                case 8:
                    d.readFromFile("vehicles.txt");
                    break;

                case 0:
                    break;

                default:
                    System.out.println("Invalid input. Please retry");
                    break;
            }

            System.out.print(System.lineSeparator() + "Press the ENTER key to continue: ");
            try {
                System.in.read();
            } catch (IOException e) {
                // you don't really want to leave this here
                e.printStackTrace();
            }
        }
    }

    private static void printMenu(){
        String tab = "\t";
        System.out.println(System.lineSeparator() + "Welcome to Franco Fortnite's dealership, how can I help you?");
        System.out.println(tab + "1. Add a car");
        System.out.println(tab + "2. Add a motorbike");
        System.out.println(tab + "3. Remove a vehicle");
        System.out.println(tab + "4. Print vehicle list");
        System.out.println(tab + "5. Print vehicle list sorted by selling price (ascending)");
        System.out.println(tab + "6. Print vehicle list sorted by selling price (descending)");
        System.out.println(tab + "7. Print vehicle list to a file");
        System.out.println(tab + "8. Get vehicle list from a file");
        System.out.println(tab + "0. Exit");
    }

    private static Vehicle inputVehicle(String type) {
        String doubleTab = "\t\t";
        Vehicle v;
        if (type.equals("car"))
            v = new Car();
        else if (type.equals("motorbike")) {
            v = new Motorbike();
        }
        else {
            throw new RuntimeException("Vehicle type not valid");
        }

        Scanner in = new Scanner(System.in);

        System.out.print(doubleTab + "Please insert " + type + " plate: ");       v.setPlate(in.nextLine());
        System.out.print(doubleTab + "Please insert " + type + " producer: ");    v.setProducer(in.nextLine());
        System.out.print(doubleTab + "Please insert " + type + " name: ");        v.setName(in.nextLine());
        System.out.print(doubleTab + "Please insert " + type + " price: ");       v.setPrice(in.nextDouble());

        return v;
    }
}