return require('packer').startup(function(use)
    use('wbthomason/packer.nvim')

    -- LSP and completion stuff
    use('neovim/nvim-lspconfig')
    use('windwp/nvim-autopairs')
    use('hrsh7th/vim-vsnip')
    use('hrsh7th/vim-vsnip-integ')
    use('hrsh7th/nvim-cmp')
    use('hrsh7th/cmp-buffer')
    use('hrsh7th/cmp-path')
    use('hrsh7th/cmp-nvim-lsp')
    use('hrsh7th/cmp-nvim-lua')
    use('hrsh7th/cmp-nvim-lsp-signature-help')
    use('williamboman/nvim-lsp-installer')
    use('onsails/lspkind.nvim')

    -- For lua language server
    -- use('tjdevries/nlua.nvim')

    -- Debugging
    use('mfussenegger/nvim-dap')
    use ({ 'rcarriga/nvim-dap-ui', requires = {'mfussenegger/nvim-dap'} })
    use('mfussenegger/nvim-dap-python')

    -- Better syntax highlighting
    use({'nvim-treesitter/nvim-treesitter', run = ':TSUpdate'})
    use('nvim-treesitter/playground')

    -- Mappings for commenting code
    use('preservim/nerdcommenter')

    -- Git integration
    use('tpope/vim-fugitive')
    use('airblade/vim-gitgutter')

    -- Telescope fuzzy finder
    use('nvim-lua/plenary.nvim')
    use('nvim-telescope/telescope.nvim')
    use('nvim-telescope/telescope-fzy-native.nvim')

    -- UI stuff
    use('gruvbox-community/gruvbox')
    use('ayu-theme/ayu-vim')
    use('vim-airline/vim-airline')

    use('rcarriga/nvim-notify')
    use('Yggdroot/indentLine')
    use('ryanoasis/vim-devicons')
    use('kyazdani42/nvim-web-devicons')
    use('norcalli/nvim-colorizer.lua')

    -- Temporary commented out
    --use('sheerun/vim-polyglot')

    --use('nvim-lua/popup.nvim')
    --use('ray-x/lsp_signature.nvim')
end)

