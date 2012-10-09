-- Code from The Haskell Road by Doets and Eijck

divides :: Integer -> Integer -> Bool
divides d n = rem n d == 0

ld :: Integer -> Integer
ld n = ldf 2 n

ldf :: Integer -> Integer -> Integer
ldf k n | divides k n = k
	| k^2 > n = n
	| otherwise = ldf (k+1) n

prime0 :: Integer -> Bool
prime0 n | n < 1 = error "not a positive integer"
	 | n == 1 = False
	 | otherwise = ld n == n

primes0 :: [Integer]
primes0 = filter prime0 [2..]

factors :: Integer -> [Integer]
factors n | n < 1 = error "not a positive integer"
	  | n == 1 = []
	  | otherwise = p : factors (div n p) where p = ld n

mnmInt :: [Int] -> Int
mnmInt [] = error "empty list"
mnmInt [x] = x
mnmInt (x:xs) = min' x (mnmInt xs)

min' :: Int -> Int -> Int
min' x y | x <= y = x
	 | otherwise = y

removeFst :: Int -> [Int] -> [Int]
removeFst m [] = []
removeFst m (x:xs) = if x == m then xs else x : (removeFst m xs)

sortInts :: [Int] -> [Int]
sortInts [] = []
sortInts lst = m : (sortInts (removeFst m lst)) where m = mnmInt lst

sortInts' [] = []
sortInts' lst = let m = mnmInt lst in m : (sortInts' (removeFst m lst))

average :: [Int] -> Rational
average [] = error "empty list"
average lst = toRational (sum' lst) / toRational (length' lst)

sum' :: [Int] -> Int
sum' [] = 0
sum' (x:xs) = x + (sum' xs)

length' :: [a] -> Int
length' [] = 0
length' (x:xs) = 1 + (length' xs)

count :: Char -> String -> Int
count c [] = 0
count c (x:xs) = let f = count c xs 
		 in 
		 if c == x then 1 + f else f

expandChar :: Char -> Int -> String
expandChar c 0 = []
expandChar c n = c : (expandChar c (n-1))

blowup :: String -> String
blowup s = blowup' 1 s

blowup' :: Int -> String -> String
blowup' pos [] = []
blowup' pos (x:xs) = (expandChar x pos) ++ (blowup' (pos+1) xs)

qsort :: Ord a => [a] -> [a]
qsort [] = []
qsort (x:xs) = (qsort (filter (< x) xs)) ++ [x] ++ (qsort (filter (>= x) xs))

prefix :: String -> String -> Bool
prefix [] ys = True
prefix (x:xs) [] = False
prefix (x:xs) (y:ys) = (x == y) && prefix xs ys

substring :: String -> String -> Bool
substring xs [] = False
substring xs ys = (prefix xs ys) || (substring xs (tail ys))

map' :: (a -> b) -> [a] -> [b]
map' f [] = []
map' f (x:xs) = f x : map f xs

lengths :: [[a]] -> [Int]
lengths [] = []
lengths (x:xs) = length x : lengths xs

lengths' :: [[a]] -> [Int]
lengths' xs = map length xs

sumLengths :: [[a]] -> Int
sumLengths xs = sum (lengths' xs)

-- filter' (>3) [1..10]
filter' :: (a -> Bool) -> [a] -> [a]
filter' p [] = []
filter' p (x:xs) | p x = x : filter' p xs 
		 | otherwise = filter' p xs

-- Faster than ld because step is by primes rather than +1
ldp :: Integer -> Integer
ldp = ldpf primes1

ldpf :: [Integer] -> Integer -> Integer
ldpf (p:ps) n | rem n p == 0 = p
	      | p^2 > n = n
	      | otherwise = ldpf ps n

primes1 :: [Integer]
primes1 = 2: filter prime [3..]

prime :: Integer -> Bool
prime n | n < 1 = error "not a positive integer"
	| n == 1 = False
	| otherwise = ldp n == n

factors' :: Integer -> [Integer]
factors' n | n < 1 = error "argument not positive"
	   | n == 1 = []
	   | otherwise = p : factors' (div n p) where p = ldp n



