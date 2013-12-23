guard 'coffeescript', input: 'ribbit/static/coffee', output: 'ribbit/static/js', bare: true

guard 'livereload' do
  watch(%r{ribbit/static/.+\.(css|js)})
  watch(%r{ribbit/templates/.+\.(html)})
end

guard :compass, configuration_file: 'config/compass_config.rb',
      compile_on_start: true do
  watch(%r{ribbit/static/.+\.(sass|scss)})
end
