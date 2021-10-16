// Insert a row into BOOKS table
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class InsertTable {
    public static void main(String[] args) throws Exception {
		Connection con = DriverManager.getConnection("jdbc:derby:c:\\dev\\java\\testdb");
		PreparedStatement ps = con.prepareStatement("insert into app.books(title,price) values(?,?)");
		ps.setString(1,"Java Comp. Ref");
		ps.setInt(2,500);
		ps.executeUpdate();

        ps.setString(1,"Python Comp. Ref");
		ps.setInt(2,250);
        ps.executeUpdate();


        ps.setString(1,"Scala Comp. Ref");
		ps.setInt(2,450);
        ps.executeUpdate();

		con.close();
	}
}