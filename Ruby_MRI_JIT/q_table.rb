class QTable
  attr_reader :state_size, :action_size, :init_qvalue
  attr_accessor :table


  def initialize(state_size, action_size, init_qvalue)
    @state_size = state_size
    @action_size = action_size
    @init_qvalue = init_qvalue
    @table = Array.new(state_size) {
      Array.new(action_size, @init_qvalue)
    }
  end
end