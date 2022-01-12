module adder (
  input   [3:0] input1,
  input   [3:0] input2,
  output  [4:0] sum
);
  assign sum = input1 + input2;
endmodule