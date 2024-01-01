import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.reflect.Array;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public class Dealer {
    private final ArrayList<Vehicle> vehicles;

    public Dealer() {
        vehicles = new ArrayList<>();
    }

    public Vehicle getVehicle(int index) {
        if(index < vehicles.size())
            return vehicles.get(index);

        // lol
        return null;
    }

    public int getVehicleCount() {
        return vehicles.size();
    }

    public void addVehicle(Vehicle v) { vehicles.add(v); }
    public void removeVehicle(Vehicle v) { vehicles.remove(v); }
    public void printVehicles() {
        if (vehicles.isEmpty()){
            System.out.println("No vehicles in the dealership at the moment. Please come back later!");
            return;
        }

        String tripleTab = "\t\t\t";

        System.out.println("Index" + tripleTab + "Plate" + tripleTab + "Producer" + tripleTab + "Name" + tripleTab + "Price");

        for (int i = 0; i < vehicles.size(); ++i){
            Vehicle v = vehicles.get(i);
            System.out.println(i + "." + tripleTab + v.getPlate() + tripleTab + v.getProducer() + tripleTab + v.getName() + tripleTab + v.getPrice());
        }

    }

    public void sortVehiclesByAscendingPrice() {
        if (!vehicles.isEmpty())
            vehicles.sort((o1, o2) -> Double.compare(o1.getPrice(), o2.getPrice()));
    }

    public void sortVehiclesByDescendingPrice() {
        if (!vehicles.isEmpty())
            vehicles.sort((o1, o2) -> Double.compare(o2.getPrice(), o1.getPrice()));
    }

    public void sumOfPrices() {
        double sum = 0;
        for (Vehicle v : vehicles){
            sum += v.getPrice();
        }

        System.out.println("Sum of prices: " + sum);
    }

    public void saveToFile(String filename) {
        StringBuilder sb = new StringBuilder();

        for (Vehicle v : vehicles)
            sb.append(v.toString()).append(System.lineSeparator());

        try (PrintWriter out = new PrintWriter(filename);){
            out.write(sb.toString());
            System.out.println("Saved vehicle list to file: " + filename);
        } catch (IOException e){
            // you don't really want to leave this here
            e.printStackTrace();
        }
    }

    public void readFromFile(String filename){
        try{
            Scanner reader = new Scanner(new File(filename));
            while(reader.hasNextLine()){
                String[] line = reader.nextLine().split(";");
                // type, plate, producer, name, price
                if(line.length == 5){
                    String type = line[0];
                    String plate = line[1];
                    String producer = line[2];
                    String name = line[3];
                    double price = Double.parseDouble(line[4]);

                    if (type.equals("car"))
                        vehicles.add(new Car(plate, producer, name, price));
                    else if (type.equals("motorbike"))
                        vehicles.add(new Motorbike(plate, producer, name, price));
                }

            }
        }
        catch (IOException e){
            // you don't really want to leave this here
            e.printStackTrace();
        }
    }
}
