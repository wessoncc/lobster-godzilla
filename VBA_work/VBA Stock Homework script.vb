Sub stock_test()
    Dim Ticker As String
    Dim Summary_Table_Row As Integer
    Dim lastrow As Long
    For Each ws In Worksheets
        ws.Activate
        lastrow = ws.Cells(Rows.Count, 1).End(xlUp).Row
        WorksheetName = ws.Name
        Summary_Table_Row = 2
        For I = 2 To lastrow
            If Cells(I + 1, 1).Value <> Cells(I, 1).Value Then
                Ticker = Cells(I, 1).Value
                Ticker_total = Ticker_total + Cells(I, 7).Value
                Range("I" & Summary_Table_Row).Value = Ticker
                Range("J" & Summary_Table_Row).Value = Ticker_total
                Summary_Table_Row = Summary_Table_Row + 1
                Ticker_total = 0
            Else
                Ticker_total = Ticker_total + Cells(I, 7).Value
            End If
        Next I
        Cells(1, 9).Value = "Ticker"
        Cells(1, 10).Value = "Total Stock Volume"
    Next ws
End Sub
