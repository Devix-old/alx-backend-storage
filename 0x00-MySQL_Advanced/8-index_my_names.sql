-- Create index named idx_name_firston names talbe with the first letter of each name

CREATE INDEX idx_name_first ON names (name(1));
