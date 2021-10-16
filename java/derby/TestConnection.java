// Connect to Apache Derby database using Embedded driver 
import java.sql.Connection;
import java.sql.DriverManager;

public class TestConnection {
	public static void main(String[] args) throws Exception {
		Connection con = DriverManager.getConnection("jdbc:derby:c:\\dev\\java\\testdb;create=true");
		System.out.println("Connected To Derby Database!");
		con.close();
	}
}