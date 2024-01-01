public class Car extends Vehicle {
    public Car() {
    }

    public Car(String plate, String producer, String name, double price) {
        super(plate, producer, name, price);
    }

    @Override
    public double getPrice() {
        double price = super.getPrice();
        double discountPercentage = 0;
        if(price > 20000)
            discountPercentage = 10;
        else if (price > 10000) {
            discountPercentage = 5;
        }
        return price - (price*discountPercentage/100);
    }

    @Override
    public String toString() {
        return "car;"+super.toString();
    }
}
