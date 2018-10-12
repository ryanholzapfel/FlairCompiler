program SIGN( n : integer ) : boolean
  begin
    return if Positive(0, n) then
              n > 0
           else
              Negative(n)
  end.