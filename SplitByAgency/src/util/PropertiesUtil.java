package util;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 *
 * @author Gaurab Pradhan
 */
public class PropertiesUtil {

    private static final String APPLICATION_PROPERTY_FILE = "conf/application.properties";

    static String username;
    static String password;
    static String dbName;
    static String dbUrl;
    static String dbTable; // distributions
    static String dbTable1; // trainings
    static String filePath;
    static String templateFile;
    static String SplitBy;

    public static String getUsername() {
        return username;
    }

    public static String getPassword() {
        return password;
    }

    public static String getDbName() {
        return dbName;
    }

    public static String getDbUrl() {
        return dbUrl;
    }

    public static String getDbTable() {
        return dbTable;
    }

    public static String getDbTable1() {
        return dbTable1;
    }
    
    public static String getFilePath() {
        return filePath;
    }

    public static String getTemplateFile() {
        return templateFile;
    }

    public static String getSplitBy() {
        return SplitBy;
    }
    
    public static void loadPropertiesFile() {

        try {
            Properties prop = new Properties();
            prop.load(new FileInputStream(APPLICATION_PROPERTY_FILE));
            username = prop.getProperty("username");
            password = prop.getProperty("password");
            dbName = prop.getProperty("dbName");
            dbUrl = prop.getProperty("dbUrl");
            dbTable = prop.getProperty("dbTable");
            dbTable1 = prop.getProperty("dbTable1");
            filePath = prop.getProperty("filePath");
            templateFile = prop.getProperty("templateFile");
            SplitBy = prop.getProperty("SplitBy");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}