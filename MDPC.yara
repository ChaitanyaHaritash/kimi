rule MDPC 
{
	meta:
		author = "@bofheaded"
		date = "24/04/2019"
		description = "YARA rules for Kimi MDPC. Used in Venom Shellcode Generator too."
		sample = "f13196cf741c65115b0c350616fcba6d"
  	strings:
  		$hex = {C2 CC 26 A3 59 3A CD AA 9F}
  	condition:
  		$hex
}
