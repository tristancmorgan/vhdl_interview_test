library ieee;
use ieee.std_logic_1164.all;

entity pipe is
    generic (
        DATA_WIDTH : positive;
        PIPE_DEPTH : natural
    );
    port ( 
        clk_i   : in std_logic;
        data_i  : in std_logic_vector(DATA_WIDTH - 1 downto 0);
        data_o  : out std_logic_vector(DATA_WIDTH - 1 downto 0)
    );
end;

architecture rtl of pipe is
    subtype data_t is std_logic_vector(DATA_WIDTH - 1 downto 0);
    type pipe_t is array (PIPE_DEPTH - 1 downto 0) of data_t;
begin
    
    g_pipe : if PIPE_DEPTH = 0 generate
        data_o <= data_i;
    elsif PIPE_DEPTH = 1 generate
        p_pipe : process (clk_i) begin
            if rising_edge(clk_i) then
                data_o <= data_i;
            end if;
        end process;
    else generate
        signal pipe : pipe_t;
    begin
        p_pipe : process (clk_i) begin
            if rising_edge(clk_i) then
                pipe(pipe'right) <= data_i;
                pipe(pipe'left downto 1) <= pipe(pipe'left - 1 downto 0);
            end if;
        end process;

        data_o <= pipe(pipe'left);
    end generate;

end;