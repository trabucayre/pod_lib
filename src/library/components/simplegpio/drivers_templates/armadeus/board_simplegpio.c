/*
 ***********************************************************************
 *
 * (c) Copyright 2008	Armadeus project
 * Fabien Marteau <fabien.marteau@armadeus.com>
 * Specific simplegpio driver for generic simplegpio driver
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 **********************************************************************
 */

#include <linux/version.h>
#if LINUX_VERSION_CODE < KERNEL_VERSION(2,6,20)
#include <linux/config.h>
#endif

/* form module/drivers */
#include <linux/init.h>
#include <linux/module.h>

/* for platform device */
#include <linux/platform_device.h>
#include <mach/hardware.h>
#ifdef CONFIG_MACH_APF27 /* To remove when MX1 platform merged */
#include <mach/fpga.h>
#endif


#include"simplegpio.h"

/*$foreach:instance$*/
static struct plat_simplegpio_port plat_simplegpio/*$instance_num$*/_data = {
	.name = "/*$instance_name$*/",
	.num=/*$instance_num$*/,
	.membase = (void *)(ARMADEUS_FPGA_BASE_ADDR_VIRT + /*$registers_base_address:swb16$*/),
	.idnum=/*$generic:id$*/,
	.idoffset=/*$register:swb16:id:offset$*/ * (16 /8)
};
/*$foreach:instance:end$*/

void plat_simplegpio_release(struct device *dev){
	PDEBUG("device %s .released\n",dev->bus_id);
}

/*$foreach:instance$*/
static struct platform_device plat_simplegpio/*$instance_num$*/_device = {
	.name = "simplegpio",
	.id=/*$instance_num$*/,
	.dev={
		.release = plat_simplegpio_release,
		.platform_data=&plat_simplegpio/*$instance_num$*/_data},
};
/*$foreach:instance:end$*/

static int __init ssimplegpio_init(void)
{
	int ret=-1;
/*$foreach:instance$*/	
	ret = platform_device_register(&plat_simplegpio/*$instance_num$*/_device);
	if(ret<0)return ret;
/*$foreach:instance:end$*/
	PDEBUG("*simplegpio inserted*\n");
	return ret;
}

static void __exit ssimplegpio_exit(void)
{
	printk(KERN_WARNING "deleting board_simplegpios\n");
/*$foreach:instance$*/	
	platform_device_unregister(&plat_simplegpio/*$instance_num$*/_device);
/*$foreach:instance:end$*/
}

module_init(ssimplegpio_init);
module_exit(ssimplegpio_exit);

MODULE_AUTHOR("Fabien Marteau <fabien.marteau@armadeus.com>");
MODULE_DESCRIPTION("Driver to blink blink some simplegpios");
MODULE_LICENSE("GPL");

