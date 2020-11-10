use 5.010;
use strict;
use warnings;


print "Enter the number1 ";
my $num1 = <STDIN>;
chomp $num1;
print "Enter the number2 ";
my $num2 = <STDIN>;
chomp $num2;
my $sum = $num1 + $num2;
print "The sum of $num1 and $num2 is $sum\n";
