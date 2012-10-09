/*
 * This is a short exercise of using Java in a functional style.
 * See main function for usage examples.
 */

public class Functional {
	// map square [1,2,3] -> [1,4,9]
	static int[] map(Fun f, int[] list) {
		int x = 0;
		int[] newList = new int[list.length];
		
		while (x < list.length) {
			Integer intObj = (Integer) (f.of(list[x]));
			newList[x] = intObj.intValue();
			x = x + 1;
		}
		
		return newList;
	}
	
	// filter even [1,2,3,4] -> [2,4,0,0]
	static int[] filter(Fun pred, int[] list) {
		int x = 0;
		int y = 0;
		int[] newList = new int[list.length];
		
		while (x < list.length) {
			Boolean boolObj = (Boolean) (pred.of(list[x]));
			if (boolObj.booleanValue()) {
				newList[y] = list[x];
				y = y + 1;
			}
			x = x + 1;
		}
		
		return newList;
	}
	
	interface Fun {
		public Object of(int x);
	}
	
	static Fun square = new Fun() {
		public Object of(int x) {
			return x*x;
		}
	};
	
	static Fun times2 = new Fun() {
		public Object of(int x) {
			return x+x;
		}
	};
	
	static Fun even = new Fun() {
		public Boolean of(int x) {
			if (x%2 == 0) {
				return true;
			} else {
				return false;
			}
		}
	};

	static int fact(int n) {
		return tfact(n, 1);
	}
	
	static int tfact(int n, int m) {
		if (n == 1) {
			return m;
		} else {
			return tfact(n-1, n*m);
		}
	}
	
	static void printList(int[] list) {
		int x = 0;
		System.out.print("[");
		while (x < (list.length - 1)) {
			System.out.print(list[x] + ", ");
			x = x + 1;
		}
		System.out.println(list[x] + "]");		
	}
	
	public static void main(String[] args) {
		int[] myList = {1,2,3,4};
		
		System.out.print("List items: ");
		printList(myList);
		
		System.out.print("List items squared: ");
		printList(map(square, myList));
		
		System.out.print("List items doubled: ");
		printList(map(times2, myList));
		
		System.out.print("List items filtered for evens: ");
		printList(filter(even, myList));
		
		// nested functions
		System.out.print("List items squared and then filtered for evens: ");
		printList(filter(even, map(square, myList)));

		// inline anonymous Fun object passed as an argument
		System.out.print("List items squared (again): ");
		printList(map(new Fun() { public Object of(int x) { return x*x; } }, myList));

		// stardard factorial function wrapped in an inline anonymous Fun object and passed as an argument
		System.out.print("List items factorial: ");
		printList(map(new Fun() { public Object of(int x) { return fact(x); } }, myList));
	}
}
