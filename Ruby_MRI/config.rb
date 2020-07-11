class Config
  attr_reader :config

  def initialize(path)
    @config = parse_config(path)
  end

  def parse_config(path)
    res = {}
    open(path) do |f|
      f.each_line do |line|
        key_value = line.chomp.split("=")
        if key_value.length != 2
          raise "invalid config line #{key_value}"
        end
        res[key_value[0]] = key_value[1]
      end
    end
    res
  end
end
