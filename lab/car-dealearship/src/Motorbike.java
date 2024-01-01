public class Motorbike extends Vehicle {
    public Motorbike() {
    }

    public Motorbike(String plate, String producer, String name, double price) {
        super(plate, producer, name, price);
    }

    @Override
    public double getPrice() {
        double price = super.getPrice();
        double discountPercentage = 0;
        if(price > 15000)
            discountPercentage = 7.5;
        else if (price > 7500) {
            discountPercentage = 3;
        }
        return price - (price*discountPercentage/100);
    }

    @Override
    public String toString() {
        return "motorbike;"+super.toString();
    }
}
