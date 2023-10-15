package finals;

public class encryotion {

//key shift by 5	
	String[] upper_case_plain = { "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
			"R", "S", "T", "U", "V", "W", "X", "Y", "Z" };
	String[] lower_case_plain = { "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
			"r", "s", "t", "u", "v", "w", "x", "y", "z" };
	String[] upper_case_encrypt = { "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
			"W", "X", "Y", "Z", "A", "B", "C", "D", "E" };
	String[] lower_case_encrypt = { "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
			"w", "x", "y", "z", "a", "b", "c", "d", "e" };

	private int get_index(String index_mes) {
		int index = -1;// case of non-Alphapatic char
		for (int i = 0; i < upper_case_plain.length; i++) {
			if (upper_case_plain[i].equals(index_mes))
				index = i;

		}
		for (int i = 0; i < lower_case_plain.length; i++) {
			if (lower_case_plain[i].equals(index_mes)) {
				index = i;
				index += 200000;
			}
		}
		return index;

	}

	public String encrypt(String message) {
		String enc_mes = "";
		for (int i = 0; i < message.length(); i++) {
			int indexed = get_index(message.charAt(i) + "");
			if (indexed == -1)// case of non-Alphapatic char
				enc_mes += message.charAt(i) + "";
			else if (indexed >= 200000) // case of lower_case-Alphapatic char
			{
				indexed -= 200000;
				enc_mes += lower_case_encrypt[indexed];
			} else // case of upper_case-Alphapatic char
			{
				enc_mes += upper_case_encrypt[indexed];
			}
		}
		return enc_mes;
	}



  public static void main(String[]args) 
  {
	  encryotion e=new encryotion();
	  String mes="Mohamed ehab";	
	  String mesenc=e.encrypt(mes);
	     System.out.println("plain message :"+mes);
	     System.out.println("encrypted message :"+mesenc);
	     
  }
}
