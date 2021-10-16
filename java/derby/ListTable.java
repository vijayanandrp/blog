// List titles from BOOKS table 
import javax.sql.rowset.CachedRowSet;
import javax.sql.rowset.RowSetFactory;
import javax.sql.rowset.RowSetProvider;

public class ListTable {
     public static void main(String[] args) throws Exception {
		RowSetFactory factory = RowSetProvider.newFactory();
		CachedRowSet crs = factory.createCachedRowSet();
		
		crs.setUrl("jdbc:derby:c:\\dev\\java\\testdb");
		crs.setCommand("select * from app.books");
		crs.execute();
		
		while(crs.next())
			 System.out.println(crs.getString("title"));
		
		crs.close();
	}
}