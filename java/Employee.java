/******************************************************************************
Design an interface called EmployeePromotion
with a method PromotionEligible () that receives five skill test marks with
common name skillsets and returns a boolean value.  

Design another interface called GradeClassify
with a method Grade (double Skillaverage) which returns a string.  

Declare an abstract class ResultAnalysis that
contains the method Analysis() receives Employee names, skill test total and
grades. This method should print the Three Topper names with skill total and
also print total number of employee with A grade, B grade and C grade


Develop a class PromotionResult which implements both EmployeePromotion
and GradeClassify; and extends the abstract class. The PromotionEligible ()  
should return true if the skillset marks of
all the five domain is greater than or equal to 50 else false. Based on the
Boolean value, the PromotionResult class should print Eligible or Not Eligible.

The main class should invoke the Grade() function only if the result is Eligible.

The Grade() returns “A” when the average of the skillset is greater than or
equal to 90, “B” if the average is between 89 and 70 and “C” if the average is
between 69 and 50.

*******************************************************************************/
interface EmployeePromotion {  
boolean PromotionEligible(int computer, int physics, int maths,
                            int chemistry, int biology);  
}  

interface GradeClassify {  
String Grade (double Skillaverage);  
}  

abstract class ResultAnalysis {  
  abstract void Analysis();  
}  


class PromotionResult  extends ResultAnalysis implements EmployeePromotion,GradeClassify {

    public boolean PromotionEligible(int computer, int physics, int maths, int chemistry, int biology)
    {
        if ((computer >= 50) && (physics >= 50) && (maths >= 50) && (chemistry >= 50) && (biology >= 50))
        {
            System.out.println("Eligible");  
            return true;
        }
        else
        {
            System.out.println("Not Eligible");  
            return false;
        }
    }
    
    public String Grade(double Skillaverage)
    {   
        String grade = "F";
        if (Skillaverage >= 90)
        {
            grade = "A";
        }
        else if ((Skillaverage <= 89) && (Skillaverage >= 70))
        {
            grade = "B";
        }
        else if ((Skillaverage <= 69) && (Skillaverage >= 50))
        {
            grade = "C";
        }
       return grade; 
    }
    
    void Analysis()
    {
        System.out.println("Analysis Done.");  
    }

}

class Employee extends PromotionResult{

   String name;
   int computer;
   int physics;
   int maths;
   int chemistry;
   int biology;
   int total;
   String grade;
   double Skillaverage;

   public Employee(String name, int computer, int physics, int maths, int chemistry, int biology) {
       this.name = name;
       this.computer = computer;
       this.physics = physics;
       this.maths = maths;
       this.chemistry = chemistry;
       this.biology = biology;
       this.grade = "F";
   }


  public void getSkillaverage() {
      total = computer + physics + chemistry + biology + maths;
      Skillaverage = (total)/5.0;
  }
  
  public void computeGrade(){
      PromotionResult tmp = new PromotionResult();
      if (tmp.PromotionEligible(computer, physics, maths, chemistry, biology) == true )
      {
          grade = tmp.Grade(Skillaverage);
      }
  }

 
  public void printEmployee() {
      System.out.println("Name:"+ name );
      System.out.println("Skillaverage:" + Skillaverage );
      System.out.println("Grade:" + grade );
      System.out.println("Total:" + total);
  }
}

public class Main
{
	public static void main(String[] args) {
	    
	    Employee obj = new Employee("Student1", 100, 80, 70, 60, 100 );
	    obj.getSkillaverage();
        obj.computeGrade();
        obj.printEmployee();
        
        System.out.println("\n");
        
        Employee obj1 = new Employee("Teacher0", 100, 80, 70, 0, 100 );
	    obj1.getSkillaverage();
        obj1.computeGrade();
        obj1.printEmployee();
	}
}
