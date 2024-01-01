public class Person {
    public final Name name;
    public final FiscalCode fiscalCode;

    public Person(String name, String fiscalCode) {
        this.name = new Name(name);
        this.fiscalCode = new FiscalCode(fiscalCode);
    }
}
