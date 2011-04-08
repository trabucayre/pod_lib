---------------------------------------------------------------------------
-- Company     : Automaticaly generated by POD
-- Author(s)   :
--
-- Creation Date : 2009-06-08
-- File          : Top_testoutput_tb.vhd
--
-- Abstract :
-- insert a description here
--
---------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

--
--                 Defines communication functions between imx and fpga:
--
--                 write procedures
--                 procedure imx_write
--                 Params :
--                 address      : Write address
--                 value        : value to write
--                 gls_clk      : clock signal
--                 imx_cs_n     : Chip select
--                 imx_oe_n     : Read signal
--                 imx_eb3_n    : Write signal
--                 imx_address  : Address signal
--                 imx_data     : Data signal
--                 WSC          : Value of imx WSC (see MC9328MXLRM.pdf p169) for sync=0
--
--                 read procedures
--                 procedure imx_read
--                 Params :
--                 address      : Write address
--                 value        : value returned
--                 gls_clk      : clock signal
--                 imx_cs_n     : Chip select
--                 imx_oe_n     : Read signal
--                 imx_eb3_n    : Write signal
--                 imx_address  : Address signal
--                 imx_data     : Data signal
--                 WSC          : Value of imx WSC (see MC9328MXLRM.pdf p169) for sync=0
--
use work.apf27_test_pkg.all;

entity top_testoutput_tb is
end entity top_testoutput_tb;

architecture RTL of top_testoutput_tb is

    CONSTANT HALF_PERIODE : time := 3.75939849624 ns;  -- Half clock period
    CONSTANT OUTPUT_CTRL_DATA : std_logic_vector := x"0000";
    CONSTANT OUTPUT_ID : std_logic_vector := x"0002";
    CONSTANT WSC : natural := 4;
    signal  imx27_wb16_wrapper00_imx_cs_n :  std_logic;
    signal  imx27_wb16_wrapper00_imx_data :  std_logic_vector(15 downto 0);
    signal  rstgen_syscon00_ext_clk :  std_logic;
    signal  imx27_wb16_wrapper00_imx_eb3_n :  std_logic;
    signal  imx27_wb16_wrapper00_imx_oe_n :  std_logic;
    signal  imx27_wb16_wrapper00_imx_address :  std_logic_vector(11 downto 0);
    signal  output_ser :  std_logic;
    signal  output_qh :  std_logic;
    signal  output_reset_n :  std_logic;
    signal  output_rclk :  std_logic;
    signal  output_srclk :  std_logic;

    component top_testoutput
    port (
        imx27_wb16_wrapper00_imx_cs_n : in std_logic;
        imx27_wb16_wrapper00_imx_data : inout std_logic_vector(15 downto 0);
        rstgen_syscon00_ext_clk : in std_logic;
        imx27_wb16_wrapper00_imx_eb3_n : in std_logic;
        imx27_wb16_wrapper00_imx_oe_n : in std_logic;
        imx27_wb16_wrapper00_imx_address : in std_logic_vector(11 downto 0);
        output_ser : out std_logic;
        output_qh : in std_logic;
        output_reset_n : out std_logic;
        output_rclk : out std_logic;
        output_srclk : out std_logic
    );
    end component top_testoutput;

    component deserializer
        port (
                 rclr_n  : in std_logic ;
                 rclk    : in std_logic ;
                 srclr_n : in std_logic ;
                 srclk   : in std_logic ;
                 ser     : in std_logic ;
                 q       : out std_logic_vector(7 downto 0);
                 qh      : out std_logic
             );
    end component deserializer;

    signal value : std_logic_vector( 15 downto 0) ;
    signal output: std_logic_vector(7 downto 0);

begin

    top : top_testoutput
    port map(
        imx27_wb16_wrapper00_imx_cs_n    => imx27_wb16_wrapper00_imx_cs_n,
        imx27_wb16_wrapper00_imx_data    => imx27_wb16_wrapper00_imx_data,
        rstgen_syscon00_ext_clk          => rstgen_syscon00_ext_clk,
        imx27_wb16_wrapper00_imx_eb3_n   => imx27_wb16_wrapper00_imx_eb3_n,
        imx27_wb16_wrapper00_imx_oe_n    => imx27_wb16_wrapper00_imx_oe_n,
        imx27_wb16_wrapper00_imx_address => imx27_wb16_wrapper00_imx_address,
        output_ser     => output_ser,
        output_qh      => output_qh,
        output_reset_n => output_reset_n,
        output_rclk    => output_rclk,
        output_srclk   => output_srclk
    );

    deserializer_p : deserializer
    port map (
        rclr_n  => output_reset_n,
        rclk    => output_rclk,
        srclr_n => output_reset_n,
        srclk   => output_srclk,
        ser     => output_ser,
        q       => output,
        qh      => output_qh
    );


    stimulis : process
    begin
        imx27_wb16_wrapper00_imx_cs_n    <= '1';
        imx27_wb16_wrapper00_imx_eb3_n   <= '1';
        imx27_wb16_wrapper00_imx_oe_n    <= '1';
        imx27_wb16_wrapper00_imx_address <= (others => '0');
        imx27_wb16_wrapper00_imx_data <= (others => 'Z');
        output_qh <= '0';
        wait for 1 us;

        -- read data
        imx_read(OUTPUT_CTRL_DATA,value,
            rstgen_syscon00_ext_clk,imx27_wb16_wrapper00_imx_cs_n,
            imx27_wb16_wrapper00_imx_oe_n,imx27_wb16_wrapper00_imx_eb3_n,
            imx27_wb16_wrapper00_imx_address,imx27_wb16_wrapper00_imx_data,
            WSC);
        report "data read :"&integer'image(to_integer(unsigned(value)))
            severity note;

        -- read id
        imx_read(OUTPUT_ID,value,
            rstgen_syscon00_ext_clk,imx27_wb16_wrapper00_imx_cs_n,
            imx27_wb16_wrapper00_imx_oe_n,imx27_wb16_wrapper00_imx_eb3_n,
            imx27_wb16_wrapper00_imx_address,imx27_wb16_wrapper00_imx_data,
            WSC);
        report "ID read :"&integer'image(to_integer(unsigned(value)))
            severity note;

        value <= x"00ca";
        wait for 1 fs;
        imx_write(OUTPUT_CTRL_DATA,value,
            rstgen_syscon00_ext_clk,imx27_wb16_wrapper00_imx_cs_n,
            imx27_wb16_wrapper00_imx_oe_n,imx27_wb16_wrapper00_imx_eb3_n,
            imx27_wb16_wrapper00_imx_address,imx27_wb16_wrapper00_imx_data,
            WSC);

        wait for 20 us;
        assert value(7 downto 0) = output
            report "Wrong value on output :"&integer'image(to_integer(unsigned(output)))&" instead of "&integer'image(to_integer(unsigned(value(7 downto 0))))
                severity warning;

        value <= x"00AC";
        wait for 1 fs;
        imx_write(OUTPUT_CTRL_DATA,value,
            rstgen_syscon00_ext_clk,imx27_wb16_wrapper00_imx_cs_n,
            imx27_wb16_wrapper00_imx_oe_n,imx27_wb16_wrapper00_imx_eb3_n,
            imx27_wb16_wrapper00_imx_address,imx27_wb16_wrapper00_imx_data,
            WSC);
        imx_write(OUTPUT_CTRL_DATA,x"00ff",
            rstgen_syscon00_ext_clk,imx27_wb16_wrapper00_imx_cs_n,
            imx27_wb16_wrapper00_imx_oe_n,imx27_wb16_wrapper00_imx_eb3_n,
            imx27_wb16_wrapper00_imx_address,imx27_wb16_wrapper00_imx_data,
            WSC);

        wait for 20 us;
        assert value(7 downto 0) = output
            report "Wrong value on output :"&integer'image(to_integer(unsigned(output)))&" instead of "&integer'image(to_integer(unsigned(value(7 downto 0))))
                severity warning;

        assert false report "End of test" severity error;
    end process stimulis;

    clockp : process
    begin
        rstgen_syscon00_ext_clk <= '1';
        wait for HALF_PERIODE;
        rstgen_syscon00_ext_clk <= '0';
        wait for HALF_PERIODE;
    end process clockp;

end architecture RTL;
