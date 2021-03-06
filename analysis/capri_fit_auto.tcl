set f [open "[lindex $::argv 0]" "r"]
set data [read $f]
close $f

set g [open "mutations_rmsd_clustal.out" "w"]
set g1 [open "mutations_rmsd_mammoth.out" "w"]

set g2 [open "mutations_rmsd_errors_clustal.out" "w"]
set g3 [open "mutations_rmsd_errors_mammoth.out" "w"]

exec mkdir -p overlay_images

puts "ENTER THE START VALUE ROW"
set start [gets stdin]
if { $start == "" } {
	set start 0
}

puts "ENTER THE END VALUE ROW"
set end [gets stdin]
set end [expr { $end * 4 }]
if { $start == "" } {
	set end [llength $data]
}

set k $start
set nv 1
set nmutc 1
set nmutm 1
while { $k < $end} {
	set wtpdb [lindex $data $k]
	set wtchain [lindex $data [expr { $k + 1 }]]
	set mutpdb [lindex $data [expr { $k + 2 }]]
	set mutchain [lindex $data [expr { $k + 3 }]]

	puts "CALCULATING RMSD BETWEEN $wtpdb AND $mutpdb"

	catch {
		exec getpdb $wtpdb
	}
	catch {
		exec getpdb $mutpdb
	}

	catch {
		exec capri-fit -iref $wtpdb.pdb $wtchain -i $mutpdb.pdb -ic $mutchain -o rmsdC -clustal -writerms
	}
	catch {
		exec capri-fit -iref $wtpdb.pdb $wtchain -i $mutpdb.pdb -ic $mutchain -o rmsdM -mammoth -writerms
	}

	# CLUSTAL VALUES

	set t1 [open "rmsdC.log" "r"]
	set data2 [read $t1]
	close $t1
	
	set data3 [split $data2 "\n"]

	set k1 0
	set count 0
	while { [lindex $data3 $k1 0] != "\$DATASUM" } {
		incr k1
		if { $k1 > [llength $data3] } {
			break
			incr count
		}
	}
	if { $count == 0 } {
		set value [lindex $data3 $k1 2]				
		if { $value != "" } {
			puts $g "$nmutc	$wtpdb $wtchain $mutpdb $mutchain	$value"
			incr nmutc
		} else {
			puts $g2 "$wtpdb $wtchain $mutpdb $mutchain" 
		}
	} else {
		puts $g2 "$wtpdb $wtchain $mutpdb $mutchain" 
	}
						
		# MAMMMOTH VALUES

	set t1 [open "rmsdM.log" "r"]
	set data2 [read $t1]
	close $t1
	
	set data3 [split $data2 "\n"]

	set k1 0
	set count 0
	while { [lindex $data3 $k1 0] != "\$DATASUM" } {
		incr k1
		if { $k1 > [llength $data3] } {
			break
			incr count
		}
	}
	if { $count == 0 } {
		set value [lindex $data3 $k1 2]
		if { $value != "" } {
			puts $g1 "$nmutm	$wtpdb $wtchain $mutpdb $mutchain	$value"
			incr nmutm
		} else {
			puts $g3 "$wtpdb $wtchain $mutpdb $mutchain" 
		}
	} else {
		puts $g3 "$wtpdb $wtchain $mutpdb $mutchain" 
	}
	catch {
		#exec mv rmsdC.pdb ./overlay_images/C.$nv.pdb
		#exec mv rmsdM.pdb ./overlay_images/M.$nv.pdb
		exec mv rmsdC-rms.out ./overlay_images/C.$nv.out
		#exec mv rmsdM-rms.out ./overlay_images/M.$nv.out
		file delete {*}[glob *.pdb]
		file delete {*}[glob *.log]
	}
	incr nv
	incr k 4
}

close $g
close $g1
close $g2
close $g3


