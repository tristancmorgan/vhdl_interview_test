library ieee;
use ieee.std_logic_1164.all;

entity reg_stage is
    generic (
        DATA_WIDTH : positive
    );
    port ( 
        clk_i   : in std_logic;

        valid_i : in std_logic;
        data_i  : in std_logic_vector(DATA_WIDTH - 1 downto 0);

        valid_o : out std_logic;
        data_o  : out std_logic_vector(DATA_WIDTH - 1 downto 0)
    );
end;

architecture rtl of reg_stage is
begin
    p_register : process (clk_i)
    begin
        if rising_edge(clk_i) then
            valid_o <= valid_i;
            data_o  <= data_i;
        end if;
    end process;
end;