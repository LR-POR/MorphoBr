# GF needs spaces between elements
{
    gsub(/./,"& ",$3) ;
    print $1,$2,$3 ;
}
