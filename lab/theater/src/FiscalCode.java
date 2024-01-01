public class FiscalCode {
    public final String fiscalCode;
    public static final String ALLOWED_FISCALCODE_FORMAT = "[A-Z]{6}[0-9]{2}[ABCDEHLMPRST][0-9]{2}[A-Z][0-9]{3}[A-Z]";

    public FiscalCode(String fiscalCode) {
        checkNotNull(fiscalCode);

        String trimmed = fiscalCode.trim().toUpperCase();

        checkNotBlank(trimmed);
        checkFormat(trimmed);

        this.fiscalCode = trimmed;
    }

    private void checkNotNull(String fiscalCode){
        if (fiscalCode == null)
            throw new RuntimeException("Fiscal code must not be null!");
    }

    private void checkNotBlank(String fiscalCode){
        if (fiscalCode.isEmpty())
            throw new RuntimeException("Fiscal code must not be blank!");
    }

    private void checkFormat(String fiscalCode){
        if (!fiscalCode.matches(ALLOWED_FISCALCODE_FORMAT))
            throw new RuntimeException("Fiscal code must match: " + ALLOWED_FISCALCODE_FORMAT);
    }
}
