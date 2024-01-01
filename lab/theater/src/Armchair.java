public class Armchair {
    private final Person occupant;
    public final char letter;
    public final int number;
    private final byte MAX_NUMBER = 40;

    public Armchair(char letter, int number, String name, String fiscalCode) {
        checkLetter(letter);
        checkNumber(number);
        this.letter = letter;
        this.number = number;
        this.occupant = new Person(name, fiscalCode);
    }

    public boolean isBusy(){
        return occupant == null;
    }

    private void checkLetter(char letter){
        if(!(letter >= 'A' && letter <= 'Y'))
            throw new RuntimeException("Letter must be between A and Y (uppercase)");
    }

    private void checkNumber(int number){
        if (number == 0 || number > MAX_NUMBER)
            throw new RuntimeException("Number must be in range [1-40] (both included)");
    }
}
