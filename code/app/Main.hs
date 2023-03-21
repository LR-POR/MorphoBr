module Main (main) where

import System.Environment ( getArgs )
import System.Exit ( exitSuccess )

import Lib ( procFile )


parse :: [String] -> IO b
parse ["-m",fn] = procFile fn >> exitSuccess
parse _ = usage >> exitSuccess

usage :: IO ()
usage = putStrLn "Usage: morpho -m FILE"

main :: IO ()
main = getArgs >>= parse

