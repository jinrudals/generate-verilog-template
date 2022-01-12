module adder (
  input   [6:0] input1,
  input   [6:0] input2,
  output  [7:0] sum
);
  assign sum = input1 + input2;
endmodule