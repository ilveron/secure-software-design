public class Vehicle {
    private String plate;
    private String producer;
    private String name;
    private double price;

    public Vehicle() { }

    public Vehicle(String plate, String producer, String name, double price) {
        this.plate = plate;
        this.producer = producer;
        this.name = name;
        this.price = price;
    }

    @Override
    public String toString() {
        return plate+";"+producer+";"+name+";"+price;
    }

    public String getPlate() {
        return plate;
    }

    public void setPlate(String plate) {
        this.plate = plate;
    }

    public String getProducer() {
        return producer;
    }

    public void setProducer(String producer) {
        this.producer = producer;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }
}
