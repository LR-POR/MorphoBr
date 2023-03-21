
module Lib (procLine, procFile) where

import Data.List.Split ( splitOn )

procLine :: String -> String
procLine s = (unwords a) ++ "\n" ++ (unwords $ ba ++ br) ++ "\n"
  where
    tk str = tail $ splitOn "" str
    ps = splitOn "\t" s
    a = tk $ head ps
    b = splitOn "+" $ head $ tail ps
    ba = tk $ head b
    br = map ("+" ++) $ tail b


procFile :: FilePath -> IO ()
procFile fp = do
  content <- readFile fp
  mapM_ putStrLn (pairs content)
  where
    pairs c = map procLine (lines c)
 
-- >>> procLine "aacheniana\taacheniano+N+F+SG"
-- "a a c h e n i a n a\na a c h e n i a n o +N +F +SG\n"
