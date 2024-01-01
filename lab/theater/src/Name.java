import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

public class Name {
    // NO MULTIPLE NAMES SUPPORT FOR NOW
    public final String name;
    public static final int NAME_MIN_LENGTH = 2;
    public static final int NAME_MAX_LENGTH = 40;
    public static final String ALLOWED_NAME_CHARACTERS = "[A-Za-z]+";

    public Name(String name) {
        checkNotNull(name);

        String trimmed = name.trim();

        checkNotBlank(trimmed);
        checkLength(trimmed);
        checkFormat(trimmed);

        this.name = trimmed;
    }

    private void checkNotNull(String name){
        if (name == null)
            throw new RuntimeException("Name must not be null!");
    }

    private void checkNotBlank(String name){
        if (name.isEmpty())
            throw new RuntimeException("Name must not be blank!");
    }

    private void checkLength(String name){
        if (name.length() < NAME_MIN_LENGTH || name.length() > NAME_MAX_LENGTH)
            throw new RuntimeException("Name length must be between 2 and 40 (both included)");
    }

    private void checkFormat(String name){
        if(!name.matches(ALLOWED_NAME_CHARACTERS))
            throw new RuntimeException("Allowed name characters are: " + ALLOWED_NAME_CHARACTERS.substring(0,ALLOWED_NAME_CHARACTERS.length()-1));
    }
}
