luasymbols=registerSymbolLookupCallback(function(str)
  if str then
    local firstchar=str:sub(1,1)
    
    if (firstchar=='\'') or (firstchar=='\"') then
      return nil
    end
  
    local c='return '..str
    local lc=loadstring(c)
    if lc then
      local isvalid,result=pcall(lc)
      if isvalid then
        return result
      else
        return nil
      end
    end
  end
end, slNotSymbol) 