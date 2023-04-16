-- SQLite
update repo
set is_very_big=true
WHERE
folder_name IN (
'marcker_dotfiles',
'NotClerks_dotfiles',
'Macmod_kewl-dotfiles',
'zeNkan_.dotfiles',
'irrenhaus_dotfiles',
'biggergeek_dotfiles',
'jalona_dotfiles',
'drussel_dotfiles',
'Max-Tweddell_configs',
'shibatanaoto_dotfiles',
'tilmitt11191_.dotfiles',
'oussoudreamer_Dotfiles',
'cyanpencil_dotfiles'
);