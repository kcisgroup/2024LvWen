 //////////////////////////////////////////////////////
///
/// Javascript port of my Actionscript Vector2 library
/// class for generic 2d vector operations and more
/// Dogan CORUH
/// 11.01.2013
/// 
//////////////////////////////////////////////////////

function MathHelper() {

}

/**
 * Converts radian to degree 将弧度转换为度
 */
MathHelper.toDegree = function (angle) {
    return angle * 180 / Math.PI;
}

/**
 * Converts degree to radian 将度转换为弧度
 */
MathHelper.toRadian = function (angle) {
    return angle * Math.PI / 180;
}

/**
 * Vector2 class for instances 实例的Vector2类
 */
function Vector2(x, y) {
    this.x = x;
    this.y = y;

    this.clone = function () {
        return new Vector2(this.x, this.y);
    }
}

/**
* Adds two vectors with each other
*/
Vector2.add = function(v1, v2) {
	return new Vector2(v1.x + v2.x, v1.y + v2.y);
}
/**
* Subtracts second vector from first vector
* @summary 用第一个向量减去第二个向量
*/
Vector2.subtract = function(v1, v2) {
	return new Vector2(v1.x - v2.x, v1.y - v2.y);
}
/**
* Multiplies vector x,y,z components with a scaler value
* @summary 用标量值乘以向量x,y,z分量
*/
Vector2.multiply = function(v, scaler) {
	return new Vector2(v.x * scaler, v.y * scaler);
}
/**
* Divides vector x,y,z components with a divider value
* @summary 用除法值对向量x,y,z分量进行除法
*/
Vector2.divide = function(v, divider) {
	return new Vector2(v.x / divider, v.y / divider);
}
/**
* Inverses vector
* @summary 逆向量
*/
Vector2.inverse = function(v) {
	return new Vector2(-v.x, -v.y);
}
/**
* sets length of given vector and return it
* @summary 设置给定向量的长度并返回它
*/
Vector2.setLength = function(v, length) {
	var len = Math.sqrt((v.x * v.x) + (v.y * v.y));
	return new Vector2(v.x * (length / len), v.y * (length / len));
}
/**
* returns true if the vector is zero vector
* @summary 如果vector为0 vector则返回true
*/
Vector2.isZeroVector = function(v) {
	return ((v.x == 0) && (v.y == 0));
}
/**
* returns the length of vector
* @summary 返回vector的长度
*/
Vector2.magnitude = function(v) {
	return Math.sqrt((v.x * v.x) + (v.y * v.y));
}
/**
* returns unit vector from given vector
* @summary 从给定的向量返回单位向量
*/
Vector2.normalize = function(v) {
	var mag = Vector2.magnitude(v);
	return new Vector2(v.x / mag, v.y / mag);
}
/**
* returns dot product of two given vectors
* @summary 返回两个给定向量的点积
*/
Vector2.dot = function(v1, v2) {
	return (v1.x * v2.x) + (v1.y * v2.y);
}
/**
* returns cross product of two given vectors
* @summary 返回两个给定向量的叉乘
*/
Vector2.cross = function(v1, v2) {
	return (v1.x * v2.y) - (v2.x * v1.y);
}
/**
* returns the distance from one vector to another
* @summary 返回从一个向量到另一个向量的距离
*/
Vector2.distance = function(v1, v2) {
	return Math.sqrt(((v1.x - v2.x) * (v1.x - v2.x)) + ((v1.y - v2.y) * (v1.y - v2.y)));
}
/**
* rotates a vector with given radian angle
* @summary 旋转具有给定弧度角的向量
* @explicit thanks to Sinan
*/
Vector2.rotateRadian = function(v, radian) {
	var vr = new Vector2();

	vr.x = v.x * Math.cos(radian) - v.y * Math.sin(radian);
	vr.y = v.y * Math.cos(radian) + v.x * Math.sin(radian);

	return vr;
}
/**
* rotates a vector with given degree angle
* @summary 旋转具有给定角度的向量
* @explicit thanks to Sinan
*/
Vector2.rotateDegree = function(v, degree) {
	return Vector2.rotateRadian(v, MathHelper.toRadian(degree));
}


/**
* returns unsigned degree angle between 0 and +180 by given two vectors
* @summary 通过给定的两个向量返回0到+180之间的无符号角度
*/
Vector2.angleUnsigned = function(v1, v2) {
	var va = Vector2.normalize(v1);
	var vb = Vector2.normalize(v2);
	var dot = Vector2.dot(va, vb);
	var rad = Math.acos(dot);
	var deg = MathHelper.toDegree(rad);

	return deg;
}
/**
* returns signed degree angle between -180 and +180 by given two vectors
* @summary 通过给定的两个向量返回-180和+180之间有符号的角度
*/
Vector2.angleSigned = function(v1, v2) {
	var va = Vector2.normalize(v1);
	var vb = Vector2.normalize(v2);
	var dot = Vector2.dot(va, vb);
	var cross = Vector2.cross(vb, va);
	var rad = Math.acos(dot);
	var deg = MathHelper.toDegree(rad);

	if (cross >= 0) {
		cross = 1;
	}
	if (cross < 0) {
		cross = -1;
	}

	return deg * cross;
}
/**
* returns degree angle between 0 and 360 by given two vectors
* @summary 通过给定的两个向量返回0到360之间的角度
*/
Vector2.angle360 = function(v1, v2) {
	var va = Vector2.normalize(v1);
	var vb = Vector2.normalize(v2);
	var dot = Vector2.dot(va, vb);
	var cross = Vector2.cross(vb, va);
	var rad = Math.acos(dot);
	var deg = MathHelper.toDegree(rad);

	if (cross > 0)
		return deg;
	else
		return 360 - deg;
}

/**
	* Compares two vectors for their equality?
	* @summary 比较两个向量是否相等?
	* @param	v1 "First vector to compare."
	* @param	v2 "Second vector to compare."
	* @return "True of false by comparison."
	*/
Vector2.isEqual = function isEqual(v1, v2)
{
	return (v1.x == v2.x) && (v1.y == v2.y);
}

Vector2.centerOfPoints = function(points) {
	var vr = new Vector2(0, 0);

	for (var i = 0; i < points.length; i++) {
		vr.x += points[i].x;
		vr.y += points[i].y;
	}

	vr.x = vr.x / points.length;
	vr.y = vr.y / points.length;

	return vr;
}

Vector2.sortPointsByAngle = function(points) {
	var angles = new Array();

	var center = Vector2.centerOfPoints(points);

	for (var i = 0; i < points.length; i++) {
		var vx = Vector2.normalize(new Vector2(1, 0));
		var v = Vector2.normalize(Vector2.subtract(center, points[i]));
		var deg = Vector2.angle360(v, vx);

		angles.push({ order: i, degree: deg, vector: points[i] });
	}

    // bubble sort
    //angles.sortOn("degree", Array.NUMERIC);
	for (var i = 0; i < angles.length; i++) {
	    for (var j = 0; j < angles.length - 1; j++) {
	        var angle1 = angles[j];
	        var angle2 = angles[j + 1];

	        if (angle1.degree > angle2.degree) {
	            var obj = angles[j];
	            angles[j] = angles[j + 1];
	            angles[j + 1] = obj;
	        }
	    }
	}

	var result = new Array();
	for (var i = 0; i < angles.length; i++)
		result.push(angles[i].vector);

	return result;
}

Vector2.areaOfPoints = function(points) {
    var fp = points[0];
    var sp;
    var fs = 0;

    for (var i = 1; i < points.length; i++) {
        sp = points[i];
        fs += (fp.x * sp.y) - (fp.y * sp.x);
        fp = points[i];
    }

    sp = points[0];
    fs += (fp.x * sp.y) - (fp.y * sp.x);
    fs = fs / 2;

    return fs;
}
