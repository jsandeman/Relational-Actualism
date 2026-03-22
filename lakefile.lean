import Lake
open Lake DSL

package «relational-actualism» {
  -- add package configuration options here
}

@[default_target]
lean_lib «RA_AQFT» {
  srcDir := "src"
}

lean_lib «RA_Complexity» {
  srcDir := "src"
}
