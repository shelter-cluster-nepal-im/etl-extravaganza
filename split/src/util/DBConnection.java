package util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 *
 * @author Gaurab Pradhan
 */
public class DBConnection {

    static String username = PropertiesUtil.getUsername();
    static String password = PropertiesUtil.getPassword();
    static String dbName = PropertiesUtil.getDbName();
    static String dbUrl = PropertiesUtil.getDbUrl();

    public static Connection getConnection() {
        Connection connection = null;
        try {
            Class.forName("org.postgresql.Driver");
            connection = DriverManager.getConnection(dbUrl + dbName, username, password);
        } catch (ClassNotFoundException e) {
            System.out.println("MySql database driver class not found." + e);
        } catch (SQLException e) {
            System.out.println("Unable to establish connection to MySql database." + e);
        }
        return connection;
    }
}
