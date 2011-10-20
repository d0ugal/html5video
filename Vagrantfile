Vagrant::Config.run do |config|

  config.vm.box = "lucid32"
  config.vm.box_url = "http://files.vagrantup.com/lucid32.box"

  config.vm.provision :chef_solo do |chef|

    chef.recipe_url = "http://cloud.github.com/downloads/d0ugal/chef_recipes/cookbooks.tar.gz"
    chef.cookbooks_path = [:vm, "cookbooks"]

    chef.add_recipe "main"
    chef.add_recipe "python"

    chef.json.merge!({

      :project_name => "html5video",

    })

  end

  config.vm.customize do |vm|
    vm.memory_size = 1020
  end

end

